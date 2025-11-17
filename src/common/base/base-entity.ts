import { PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn, Column } from 'typeorm'
import { ApiProperty } from '@nestjs/swagger'

/**
 * Base entity class with common fields
 * All entities should extend this class to get:
 * - id (UUID)
 * - createdAt (timestamp)
 * - updatedAt (timestamp)
 */
export abstract class BaseEntity {
  @ApiProperty({
    description: 'Unique entity ID (UUID)',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  @PrimaryGeneratedColumn('uuid')
  id: string

  @ApiProperty({
    description: 'Creation date',
    example: '2024-01-01T00:00:00.000Z',
  })
  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date

  @ApiProperty({
    description: 'Last update date',
    example: '2024-01-01T00:00:00.000Z',
  })
  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date
}


