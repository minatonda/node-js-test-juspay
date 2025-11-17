import { ApiProperty } from '@nestjs/swagger'
import { IsArray, IsNotEmpty, IsOptional, IsString, MaxLength } from 'class-validator'

export class CreateNoteDto {
  @ApiProperty({
    description: 'Note title',
    example: 'My first note',
    maxLength: 255,
  })
  @IsString()
  @IsNotEmpty()
  @MaxLength(255)
  title: string

  @ApiProperty({
    description: 'Note content/body',
    example: 'This is the content of my note...',
  })
  @IsString()
  @IsNotEmpty()
  body: string

  @ApiProperty({
    description: 'Optional tags for categorization',
    example: ['work', 'important'],
    required: false,
    type: [String],
  })
  @IsArray()
  @IsOptional()
  @IsString({ each: true })
  tags?: string[]
}

