/**
 * Pagination utility functions
 * Provides consistent pagination calculations across all endpoints
 */

export interface PaginationParams {
  page: number
  limit: number
}

export interface PaginationResult<T> {
  items: T[]
  total: number
  page: number
  limit: number
  pageCount: number
}

/**
 * Normalizes pagination parameters to ensure valid values
 * @param page - Page number (optional, defaults to 1)
 * @param limit - Items per page (optional, defaults to 20)
 * @returns Normalized pagination parameters
 */
export function normalizePaginationParams(page?: number, limit?: number): PaginationParams {
  const normalizedPage = page && page > 0 ? page : 1
  const normalizedLimit = limit && limit > 0 ? limit : 20

  return {
    page: normalizedPage,
    limit: normalizedLimit,
  }
}

/**
 * Calculates the total number of pages
 * @param total - Total number of items
 * @param limit - Items per page
 * @returns Total number of pages (minimum 1)
 */
export function calculatePageCount(total: number, limit: number): number {
  if (total === 0 || limit === 0) {
    return 1
  }
  return Math.ceil(total / limit)
}

/**
 * Creates a paginated response object
 * @param items - Array of items for the current page
 * @param total - Total number of items (before pagination)
 * @param page - Current page number
 * @param limit - Items per page
 * @returns Paginated response object
 */
export function createPaginationResponse<T>(
  items: T[],
  total: number,
  page: number,
  limit: number,
): PaginationResult<T> {
  return {
    items,
    total,
    page,
    limit,
    pageCount: calculatePageCount(total, limit),
  }
}


