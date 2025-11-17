import { ApiProperty } from '@nestjs/swagger'
import { IsArray, IsOptional, IsString, MaxLength } from 'class-validator'

export class UpdateNoteDto {
  @ApiProperty({
    description: 'Note title',
    example: 'Updated title',
    maxLength: 255,
    required: false,
  })
  @IsString()
  @IsOptional()
  @MaxLength(255)
  title?: string

  @ApiProperty({
    description: 'Note content/body',
    example: 'Updated content...',
    required: false,
  })
  @IsString()
  @IsOptional()
  body?: string

  @ApiProperty({
    description: 'Optional tags for categorization',
    example: ['work', 'important', 'urgent'],
    required: false,
    type: [String],
  })
  @IsArray()
  @IsOptional()
  @IsString({ each: true })
  tags?: string[]
}

