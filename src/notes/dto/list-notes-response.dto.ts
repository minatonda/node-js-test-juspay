import { ApiProperty } from '@nestjs/swagger'
import { PaginationResponseDto } from '../../common/dto/pagination-response.dto'
import { NoteEntity } from '../note.entity'

export class ListNotesResponseDto extends PaginationResponseDto<NoteEntity> {
  @ApiProperty({
    description: 'List of notes',
    type: [NoteEntity],
  })
  items: NoteEntity[]
}

