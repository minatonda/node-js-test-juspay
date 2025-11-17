import { SelectQueryBuilder, FindOptionsWhere, IsNull } from 'typeorm'
import { ISoftDeletable } from '../interfaces/soft-deletable.interface'

/**
 * Soft delete utility functions
 * Provides consistent soft delete behavior across the application
 */

/**
 * Applies soft delete filter to a query builder
 * Excludes entities where deletedAt IS NOT NULL
 * 
 * @param queryBuilder - TypeORM query builder
 * @param alias - Entity alias used in the query builder
 */
export function applySoftDeleteFilter<T>(
  queryBuilder: SelectQueryBuilder<T>,
  alias: string = 'entity',
): void {
  queryBuilder.andWhere(`${alias}.deletedAt IS NULL`)
}

/**
 * Adds soft delete condition to a where clause
 * Excludes entities where deletedAt IS NOT NULL
 * 
 * @param where - Existing where clause
 * @returns Where clause with soft delete filter added
 */
export function excludeDeleted<T>(
  where: FindOptionsWhere<T> = {} as FindOptionsWhere<T>,
): FindOptionsWhere<T> {
  return {
    ...where,
    deletedAt: IsNull(),
  } as FindOptionsWhere<T>
}

/**
 * Performs soft delete on an entity
 * Sets deletedAt to current date
 * 
 * @param entity - Entity to soft delete
 */
export function performSoftDelete(entity: ISoftDeletable): void {
  entity.deletedAt = new Date()
}

/**
 * Checks if an entity is soft deleted
 * 
 * @param entity - Entity to check
 * @returns true if entity is soft deleted, false otherwise
 */
export function isSoftDeleted(entity: ISoftDeletable): boolean {
  return entity.deletedAt !== null && entity.deletedAt !== undefined
}

