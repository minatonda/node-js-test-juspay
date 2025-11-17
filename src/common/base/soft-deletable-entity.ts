import { Column, Index } from 'typeorm'
import { ApiProperty } from '@nestjs/swagger'
import { BaseEntity } from './base-entity'
import { ISoftDeletable } from '../interfaces/soft-deletable.interface'

/**
 * Base entity class with soft delete support
 * Extends BaseEntity and adds deletedAt field
 * All entities that need soft delete should extend this class
 */
@Index(['deletedAt'])
export abstract class SoftDeletableEntity extends BaseEntity implements ISoftDeletable {
  @ApiProperty({
    description: 'Deletion date (soft delete)',
    example: null,
    required: false,
  })
  @Column({ name: 'deleted_at', type: 'datetime', nullable: true })
  deletedAt?: Date | null
}


