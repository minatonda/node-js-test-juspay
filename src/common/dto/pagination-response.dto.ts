import { ApiProperty } from '@nestjs/swagger'

/**
 * Base DTO for paginated responses.
 * All endpoints that return paginated data should use this structure.
 * 
 * @template T - The type of items in the paginated response
 */
export class PaginationResponseDto<T> {
  @ApiProperty({
    description: 'List of items',
    isArray: true,
  })
  items: T[]

  @ApiProperty({
    description: 'Total number of items (before pagination)',
    example: 100,
  })
  total: number

  @ApiProperty({
    description: 'Current page number',
    example: 1,
  })
  page: number

  @ApiProperty({
    description: 'Number of items per page',
    example: 20,
  })
  limit: number

  @ApiProperty({
    description: 'Total number of pages',
    example: 5,
  })
  pageCount: number
}


