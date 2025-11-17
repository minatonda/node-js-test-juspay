import { ApiProperty } from '@nestjs/swagger'
import {
  Column,
  Entity,
  Index,
  BeforeInsert,
  BeforeUpdate,
} from 'typeorm'
import { SoftDeletableEntity } from '../common/base/soft-deletable-entity'

@Entity({ name: 'notes' })
@Index(['title']) // Index for search
export class NoteEntity extends SoftDeletableEntity {

  @ApiProperty({
    description: 'Note title',
    example: 'My first note',
    maxLength: 255,
  })
  @Column({ type: 'text' })
  title: string

  @ApiProperty({
    description: 'Note content/body',
    example: 'This is the content of my note...',
  })
  @Column({ type: 'text' })
  body: string

  @ApiProperty({
    description: 'Tags for categorization',
    example: ['work', 'important'],
    type: [String],
  })
  @Column({
    type: 'text',
    nullable: false,
    transformer: {
      to: (value: string[]) => {
        // Ensure we always return a valid JSON string
        if (Array.isArray(value)) {
          return JSON.stringify(value)
        }
        if (typeof value === 'string') {
          // If already a string, it could be JSON or a simple string
          try {
            JSON.parse(value)
            return value // Already valid JSON
          } catch {
            return JSON.stringify([value]) // Convert simple string to array
          }
        }
        return JSON.stringify([])
      },
      from: (value: string) => {
        try {
          if (!value || value === '') {
            return []
          }
          const parsed = JSON.parse(value)
          return Array.isArray(parsed) ? parsed : []
        } catch {
          return []
        }
      },
    },
  })
  tags: string[] = []

  @BeforeInsert()
  @BeforeUpdate()
  ensureTagsIsArray() {
    // Ensure tags is always an array before saving
    if (!Array.isArray(this.tags)) {
      this.tags = []
    }
  }
}

