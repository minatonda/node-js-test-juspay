import { ApiProperty } from '@nestjs/swagger'
import { IsArray, IsEnum, IsOptional, IsString } from 'class-validator'
import { Transform } from 'class-transformer'
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto'

export enum SortBy {
  CREATED_AT = 'createdAt',
  UPDATED_AT = 'updatedAt',
  TITLE = 'title',
}

export enum SortOrder {
  ASC = 'ASC',
  DESC = 'DESC',
}

export class ListNotesQueryDto extends PaginationQueryDto {

  @ApiProperty({
    description: 'Search by keywords in title or content',
    example: 'important',
    required: false,
  })
  @IsString()
  @IsOptional()
  search?: string

  @ApiProperty({
    description: 'Filter by tags (returns notes that contain any of the provided tags)',
    example: ['work', 'important'],
    required: false,
    type: [String],
  })
  @Transform(({ value }) => {
    if (Array.isArray(value)) {
      return value
    }
    if (typeof value === 'string') {
      return [value]
    }
    return value
  })
  @IsArray()
  @IsOptional()
  @IsString({ each: true })
  tags?: string[]

  @ApiProperty({
    description: 'Field for sorting',
    enum: SortBy,
    example: SortBy.CREATED_AT,
    required: false,
    default: SortBy.CREATED_AT,
  })
  @IsEnum(SortBy)
  @IsOptional()
  sortBy?: SortBy = SortBy.CREATED_AT

  @ApiProperty({
    description: 'Sort order',
    enum: SortOrder,
    example: SortOrder.DESC,
    required: false,
    default: SortOrder.DESC,
  })
  @IsEnum(SortOrder)
  @IsOptional()
  sortOrder?: SortOrder = SortOrder.DESC
}

