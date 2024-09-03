use std::{
    cmp::Ordering,
    fmt,
    ops::{Range, RangeFrom, RangeFull, RangeInclusive, RangeTo, RangeToInclusive},
};

use ahash::AHashMap;
use itertools::Itertools;
use thiserror::Error;

mod characters;
#[cfg(feature = "tokenizers")]
mod huggingface;
#[cfg(feature = "rust-tokenizers")]
mod rust_tokenizers;
#[cfg(feature = "tiktoken-rs")]
mod tiktoken;

use crate::trim::Trim;
pub use characters::Characters;

/// Indicates there was an error with the chunk capacity configuration.
/// The `Display` implementation will provide a human-readable error message to
/// help debug the issue that caused the error.
#[derive(Error, Debug)]
#[error(transparent)]
pub struct ChunkCapacityError(#[from] ChunkCapacityErrorRepr);

/// Private error and free to change across minor version of the crate.
#[derive(Error, Debug)]
enum ChunkCapacityErrorRepr {
    #[error("Max chunk size must be greater than or equal to the desired chunk size")]
    MaxLessThanDesired,
}

/// Describes the valid chunk size(s) that can be generated.
///
/// The `desired` size is the target size for the chunk. In most cases, this
/// will also serve as the maximum size of the chunk. It is always possible
/// that a chunk may be returned that is less than the `desired` value, as
/// adding the next piece of text may have made it larger than the `desired`
/// capacity.
///
/// The `max` size is the maximum possible chunk size that can be generated.
/// By setting this to a larger value than `desired`, it means that the chunk
/// should be as close to `desired` as possible, but can be larger if it means
/// staying at a larger semantic level.
///
/// The splitter will consume text until at maxumum somewhere between `desired`
/// and `max`, if they differ, but never above `max`.
///
/// If you need to ensure a fixed size, set `desired` and `max` to the same
/// value. For example, if you are trying to maximize the context window for an
/// embedding.
///
/// If you are loosely targeting a size, but have some extra room, for example
/// in a RAG use case where you roughly want a certain part of a document, you
/// can set `max` to your absolute maxumum, and the splitter can stay at a
/// higher semantic level when determining the chunk.
#[derive(Copy, Clone, Debug, PartialEq)]
pub struct ChunkCapacity {
    desired: usize,
    max: usize,
}

impl ChunkCapacity {
    /// Create a new `ChunkCapacity` with the same `desired` and `max` size.
    #[must_use]
    pub fn new(size: usize) -> Self {
        Self {
            desired: size,
            max: size,
        }
    }

    /// The `desired` size is the target size for the chunk. In most cases, this
    /// will also serve as the maximum size of the chunk. It is always possible
    /// that a chunk may be returned that is less than the `desired` value, as
    /// adding the next piece of text may have made it larger than the `desired`
    /// capacity.
    #[must_use]
    pub fn desired(&self) -> usize {
        self.desired
    }

    /// The `max` size is the maximum possible chunk size that can be generated.
    /// By setting this to a larger value than `desired`, it means that the chunk
    /// should be as close to `desired` as possible, but can be larger if it means
    /// staying at a larger semantic level.
    #[must_use]
    pub fn max(&self) -> usize {
        self.max
    }

    /// If you need to ensure a fixed size, set `desired` and `max` to the same
    /// value. For example, if you are trying to maximize the context window for an
    /// embedding.
    ///
    /// If you are loosely targeting a size, but have some extra room, for example
    /// in a RAG use case where you roughly want a certain part of a document, you
    /// can set `max` to your absolute maxumum, and the splitter can stay at a
    /// higher semantic level when determining the chunk.
    ///
    /// # Errors
    ///
    /// If the `max` size is less than the `desired` size, an error is returned.
    pub fn with_max(mut self, max: usize) -> Result<Self, ChunkCapacityError> {
        if max < self.desired {
            Err(ChunkCapacityError(
                ChunkCapacityErrorRepr::MaxLessThanDesired,
            ))
        } else {
            self.max = max;
            Ok(self)
        }
    }

    /// Validate if a given chunk fits within the capacity
    ///
    /// - `Ordering::Less` indicates more could be added
    /// - `Ordering::Equal` indicates the chunk is within the capacity range
    /// - `Ordering::Greater` indicates the chunk is larger than the capacity
    #[must_use]
    pub fn fits(&self, chunk_size: usize) -> Ordering {
        if chunk_size < self.desired {
            Ordering::Less
        } else if chunk_size > self.max {
            Ordering::Greater
        } else {
            Ordering::Equal
        }
    }

    /// Generates a chunk size object based on the size provided from a sizer
    /// Calculates and stores whether or not it fits within the capacity
    #[must_use]
    fn chunk_size(&self, size: usize) -> ChunkSize {
        ChunkSize::new(self.fits(size), size)
    }
}

impl From<usize> for ChunkCapacity {
    fn from(size: usize) -> Self {
        ChunkCapacity::new(size)
    }
}

impl From<Range<usize>> for ChunkCapacity {
    fn from(range: Range<usize>) -> Self {
        ChunkCapacity::new(range.start)
            .with_max(range.end.saturating_sub(1).max(range.start))
            .expect("invalid range")
    }
}

impl From<RangeFrom<usize>> for ChunkCapacity {
    fn from(range: RangeFrom<usize>) -> Self {
        ChunkCapacity::new(range.start)
            .with_max(usize::MAX)
            .expect("invalid range")
    }
}

impl From<RangeFull> for ChunkCapacity {
    fn from(_: RangeFull) -> Self {
        ChunkCapacity::new(usize::MIN)
            .with_max(usize::MAX)
            .expect("invalid range")
    }
}

impl From<RangeInclusive<usize>> for ChunkCapacity {
    fn from(range: RangeInclusive<usize>) -> Self {
        ChunkCapacity::new(*range.start())
            .with_max(*range.end())
            .expect("invalid range")
    }
}

impl From<RangeTo<usize>> for ChunkCapacity {
    fn from(range: RangeTo<usize>) -> Self {
        ChunkCapacity::new(usize::MIN)
            .with_max(range.end.saturating_sub(1))
            .expect("invalid range")
    }
}

impl From<RangeToInclusive<usize>> for ChunkCapacity {
    fn from(range: RangeToInclusive<usize>) -> Self {
        ChunkCapacity::new(usize::MIN)
            .with_max(range.end)
            .expect("invalid range")
    }
}

/// Result returned from a `ChunkSizer`. Includes the size of the chunk, in units
/// determined by the sizer, as well as the max byte offset of the text that
/// would fit within the given `ChunkCapacity`.
#[derive(Copy, Clone, Debug, PartialEq)]
pub struct ChunkSize {
    /// Whether or not the entire chunk fits within the `ChunkCapacity`
    fits: Ordering,
    /// Size of the chunk, in units used by the sizer.
    size: usize,
}

impl ChunkSize {
    #[must_use]
    pub fn new(fits: Ordering, size: usize) -> Self {
        Self { fits, size }
    }

    /// Determine whether the chunk size fits within the capacity or not
    #[must_use]
    pub fn fits(&self) -> Ordering {
        self.fits
    }

    /// Size of the chunk, in units used by the sizer.
    #[must_use]
    pub fn size(&self) -> usize {
        self.size
    }
}

/// Determines the size of a given chunk.
pub trait ChunkSizer {
    /// Determine the size of a given chunk to use for validation
    fn size(&self, chunk: &str) -> usize;
}

/// Indicates there was an error with the chunk configuration.
/// The `Display` implementation will provide a human-readable error message to
/// help debug the issue that caused the error.
#[derive(Error, Debug)]
#[error(transparent)]
pub struct ChunkConfigError(#[from] ChunkConfigErrorRepr);

/// Private error and free to change across minor version of the crate.
#[derive(Error, Debug)]
enum ChunkConfigErrorRepr {
    #[error("The overlap is larger than or equal to the desired chunk capacity")]
    OverlapLargerThanCapacity,
}

/// Configuration for how chunks should be created
#[derive(Debug)]
pub struct ChunkConfig<Sizer>
where
    Sizer: ChunkSizer,
{
    /// The chunk capacity to use for filling chunks
    capacity: ChunkCapacity,
    /// The amount of overlap between chunks. Defaults to 0.
    overlap: usize,
    /// The chunk sizer to use for determining the size of each chunk
    sizer: Sizer,
    /// Whether whitespace will be trimmed from the beginning and end of each chunk
    trim: bool,
}

impl ChunkConfig<Characters> {
    /// Create a basic configuration for chunking with only the required value a chunk capacity.
    ///
    /// By default, chunk sizes will be calculated based on the number of characters in each chunk.
    /// You can set a custom chunk sizer by calling [`Self::with_sizer`].
    ///
    /// By default, chunks will be trimmed. If you want to preserve whitespace,
    /// call [`Self::with_trim`] and set it to `false`.
    #[must_use]
    pub fn new(capacity: impl Into<ChunkCapacity>) -> Self {
        Self {
            capacity: capacity.into(),
            overlap: 0,
            sizer: Characters,
            trim: true,
        }
    }
}

impl<Sizer> ChunkConfig<Sizer>
where
    Sizer: ChunkSizer,
{
    /// Retrieve a reference to the chunk capacity for this configuration.
    pub fn capacity(&self) -> &ChunkCapacity {
        &self.capacity
    }

    /// Retrieve the amount of overlap between chunks.
    pub fn overlap(&self) -> usize {
        self.overlap
    }

    /// Set the amount of overlap between chunks.
    ///
    /// # Errors
    ///
    /// Will return an error if the overlap is larger than or equal to the chunk capacity.
    pub fn with_overlap(mut self, overlap: usize) -> Result<Self, ChunkConfigError> {
        if overlap >= self.capacity.desired {
            Err(ChunkConfigError(
                ChunkConfigErrorRepr::OverlapLargerThanCapacity,
            ))
        } else {
            self.overlap = overlap;
            Ok(self)
        }
    }

    /// Retrieve a reference to the chunk sizer for this configuration.
    pub fn sizer(&self) -> &Sizer {
        &self.sizer
    }

    /// Set a custom chunk sizer to use for determining the size of each chunk
    ///
    /// ```
    /// use text_splitter::{Characters, ChunkConfig};
    ///
    /// let config = ChunkConfig::new(512).with_sizer(Characters);
    /// ```
    #[must_use]
    pub fn with_sizer<S: ChunkSizer>(self, sizer: S) -> ChunkConfig<S> {
        ChunkConfig {
            capacity: self.capacity,
            overlap: self.overlap,
            sizer,
            trim: self.trim,
        }
    }

    /// Whether chunkd should have whitespace trimmed from the beginning and end or not.
    pub fn trim(&self) -> bool {
        self.trim
    }

    /// Specify whether chunks should have whitespace trimmed from the
    /// beginning and end or not.
    ///
    /// If `false` (default), joining all chunks should return the original
    /// string.
    /// If `true`, all chunks will have whitespace removed from beginning and end.
    ///
    /// ```
    /// use text_splitter::ChunkConfig;
    ///
    /// let config = ChunkConfig::new(512).with_trim(false);
    /// ```
    #[must_use]
    pub fn with_trim(mut self, trim: bool) -> Self {
        self.trim = trim;
        self
    }
}

impl<T> From<T> for ChunkConfig<Characters>
where
    T: Into<ChunkCapacity>,
{
    fn from(capacity: T) -> Self {
        Self::new(capacity)
    }
}

/// A memoized chunk sizer that caches the size of chunks.
/// Very helpful when the same chunk is being validated multiple times, which
/// happens often, and can be expensive to compute, such as with tokenizers.
#[derive(Debug)]
pub struct MemoizedChunkSizer<'sizer, Sizer>
where
    Sizer: ChunkSizer,
{
    /// Cache of chunk sizes per byte offset range for base capacity
    capacity_cache: AHashMap<Range<usize>, ChunkSize>,
    /// The configuration for the chunk sizer
    chunk_config: &'sizer ChunkConfig<Sizer>,
    /// Cache of chunk sizes per byte offset range for overlap ranges
    overlap_cache: AHashMap<Range<usize>, ChunkSize>,
    /// Semantic level, used for determining trimming behavior
    trim: Trim,
}

impl<'sizer, Sizer> MemoizedChunkSizer<'sizer, Sizer>
where
    Sizer: ChunkSizer,
{
    /// Wrap any chunk sizer for memoization
    pub fn new(chunk_config: &'sizer ChunkConfig<Sizer>, trim: Trim) -> Self {
        Self {
            capacity_cache: AHashMap::new(),
            chunk_config,
            overlap_cache: AHashMap::new(),
            trim,
        }
    }

    /// Determine the size of a given chunk to use for validation,
    /// returning a cached value if it exists, and storing the result if not.
    fn chunk_size(&mut self, offset: usize, chunk: &str, is_overlap: bool) -> ChunkSize {
        let cache = if is_overlap {
            &mut self.overlap_cache
        } else {
            &mut self.capacity_cache
        };
        let capacity = if is_overlap {
            self.chunk_config.overlap.into()
        } else {
            self.chunk_config.capacity
        };

        *cache
            .entry(offset..(offset + chunk.len()))
            .or_insert_with(|| capacity.chunk_size(self.chunk_config.sizer.size(chunk)))
    }

    /// Check if the chunk is within the capacity. Chunk should be trimmed if necessary beforehand.
    pub fn check_capacity(&mut self, offset: usize, chunk: &str, is_overlap: bool) -> ChunkSize {
        let (offset, chunk) = self.trim_chunk(offset, chunk);
        self.chunk_size(offset, chunk, is_overlap)
    }

    /// If trim chunks is on, trim the str and adjust the offset
    pub fn trim_chunk<'text>(&self, offset: usize, chunk: &'text str) -> (usize, &'text str) {
        if self.chunk_config.trim {
            self.trim.trim(offset, chunk)
        } else {
            (offset, chunk)
        }
    }

    /// Find the best level to start splitting the text
    pub fn find_correct_level<'text, L: fmt::Debug>(
        &mut self,
        offset: usize,
        levels_with_first_chunk: impl Iterator<Item = (L, &'text str)>,
    ) -> (Option<L>, Option<usize>) {
        let mut semantic_level = None;
        let mut max_offset = None;
        let max_size = self.chunk_config.capacity.max;

        // We assume that larger levels are also longer. We can skip lower levels if going to a higher level would result in a shorter text
        let levels_with_first_chunk =
            levels_with_first_chunk.coalesce(|(a_level, a_str), (b_level, b_str)| {
                if a_str.len() >= b_str.len() {
                    Ok((b_level, b_str))
                } else {
                    Err(((a_level, a_str), (b_level, b_str)))
                }
            });

        for (level, str) in levels_with_first_chunk {
            // Skip tokenizing levels that we know are too small anyway.
            let len = str.len();
            if len > max_size {
                let chunk_size = self.check_capacity(offset, str, false);
                // If this no longer fits, we use the level we are at.
                if chunk_size.fits.is_gt() {
                    max_offset = Some(offset + len);
                    break;
                }
            }
            // Otherwise break up the text with the next level
            semantic_level = Some(level);
        }

        (semantic_level, max_offset)
    }

    /// Clear the cached values. Once we've moved the cursor,
    /// we don't need to keep the old values around.
    pub fn clear_cache(&mut self) {
        self.capacity_cache.clear();
        self.overlap_cache.clear();
    }
}

#[cfg(test)]
mod tests {
    use std::sync::atomic::{self, AtomicUsize};

    use crate::trim::Trim;

    use super::*;

    #[test]
    fn check_chunk_capacity() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(4)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(5)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(6)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Less
        );
    }

    #[test]
    fn check_chunk_capacity_for_range() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(0..0)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(0..5)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(5..6)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(6..100)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Less
        );
    }

    #[test]
    fn check_chunk_capacity_for_range_from() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(0..)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(5..)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(6..)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Less
        );
    }

    #[test]
    fn check_chunk_capacity_for_range_full() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(..)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
    }

    #[test]
    fn check_chunk_capacity_for_range_inclusive() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(0..=4)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(5..=6)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(4..=5)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(6..=100)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Less
        );
    }

    #[test]
    fn check_chunk_capacity_for_range_to() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(..0)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(..5)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(..6)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
    }

    #[test]
    fn check_chunk_capacity_for_range_to_inclusive() {
        let chunk = "12345";

        assert_eq!(
            ChunkCapacity::from(..=4)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Greater
        );
        assert_eq!(
            ChunkCapacity::from(..=5)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
        assert_eq!(
            ChunkCapacity::from(..=6)
                .chunk_size(Characters.size(chunk))
                .fits,
            Ordering::Equal
        );
    }

    #[derive(Default)]
    struct CountingSizer {
        calls: AtomicUsize,
    }

    impl ChunkSizer for CountingSizer {
        // Return character version, but count calls
        fn size(&self, chunk: &str) -> usize {
            self.calls.fetch_add(1, atomic::Ordering::SeqCst);
            Characters.size(chunk)
        }
    }

    #[test]
    fn memoized_sizer_only_calculates_once_per_text() {
        let chunk_config = ChunkConfig::new(10).with_sizer(CountingSizer::default());
        let mut memoized_sizer = MemoizedChunkSizer::new(&chunk_config, Trim::All);
        let text = "1234567890";
        for _ in 0..10 {
            memoized_sizer.chunk_size(0, text, false);
        }

        assert_eq!(
            memoized_sizer
                .chunk_config
                .sizer()
                .calls
                .load(atomic::Ordering::SeqCst),
            1
        );
    }

    #[test]
    fn memoized_sizer_calculates_once_per_different_text() {
        let chunk_config = ChunkConfig::new(10).with_sizer(CountingSizer::default());
        let mut memoized_sizer = MemoizedChunkSizer::new(&chunk_config, Trim::All);
        let text = "1234567890";
        for i in 0..10 {
            memoized_sizer.chunk_size(0, text.get(0..i).unwrap(), false);
        }

        assert_eq!(
            memoized_sizer
                .chunk_config
                .sizer()
                .calls
                .load(atomic::Ordering::SeqCst),
            10
        );
    }

    #[test]
    fn can_clear_cache_on_memoized_sizer() {
        let chunk_config = ChunkConfig::new(10).with_sizer(CountingSizer::default());
        let mut memoized_sizer = MemoizedChunkSizer::new(&chunk_config, Trim::All);
        let text = "1234567890";
        for _ in 0..10 {
            memoized_sizer.chunk_size(0, text, false);
            memoized_sizer.clear_cache();
        }

        assert_eq!(
            memoized_sizer
                .chunk_config
                .sizer()
                .calls
                .load(atomic::Ordering::SeqCst),
            10
        );
    }

    #[test]
    fn basic_chunk_config() {
        let config = ChunkConfig::new(10);
        assert_eq!(config.capacity, 10.into());
        assert_eq!(config.sizer, Characters);
        assert!(config.trim());
    }

    #[test]
    fn disable_trimming() {
        let config = ChunkConfig::new(10).with_trim(false);
        assert!(!config.trim());
    }

    #[test]
    fn new_sizer() {
        #[derive(Debug, PartialEq)]
        struct BasicSizer;

        impl ChunkSizer for BasicSizer {
            fn size(&self, _chunk: &str) -> usize {
                unimplemented!()
            }
        }

        let config = ChunkConfig::new(10).with_sizer(BasicSizer);
        assert_eq!(config.capacity, 10.into());
        assert_eq!(config.sizer, BasicSizer);
        assert!(config.trim());
    }

    #[test]
    fn chunk_capacity_max_and_desired_equal() {
        let capacity = ChunkCapacity::new(10);
        assert_eq!(capacity.desired(), 10);
        assert_eq!(capacity.max(), 10);
    }

    #[test]
    fn chunk_capacity_can_adjust_max() {
        let capacity = ChunkCapacity::new(10).with_max(20).unwrap();
        assert_eq!(capacity.desired(), 10);
        assert_eq!(capacity.max(), 20);
    }

    #[test]
    fn chunk_capacity_max_cant_be_less_than_desired() {
        let capacity = ChunkCapacity::new(10);
        let err = capacity.with_max(5).unwrap_err();
        assert_eq!(
            err.to_string(),
            "Max chunk size must be greater than or equal to the desired chunk size"
        );
        assert_eq!(capacity.desired(), 10);
        assert_eq!(capacity.max(), 10);
    }

    #[test]
    fn set_chunk_overlap() {
        let config = ChunkConfig::new(10).with_overlap(5).unwrap();
        assert_eq!(config.overlap(), 5);
    }

    #[test]
    fn cant_set_overlap_larger_than_capacity() {
        let chunk_config = ChunkConfig::new(5);
        let err = chunk_config.with_overlap(10).unwrap_err();
        assert_eq!(
            err.to_string(),
            "The overlap is larger than or equal to the desired chunk capacity"
        );
    }

    #[test]
    fn cant_set_overlap_larger_than_desired() {
        let chunk_config = ChunkConfig::new(5..15);
        let err = chunk_config.with_overlap(10).unwrap_err();
        assert_eq!(
            err.to_string(),
            "The overlap is larger than or equal to the desired chunk capacity"
        );
    }
}
