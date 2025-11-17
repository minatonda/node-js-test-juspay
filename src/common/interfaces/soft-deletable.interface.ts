/**
 * Interface for entities that support soft delete
 */
export interface ISoftDeletable {
  deletedAt?: Date | null
}

/**
 * Type guard to check if an entity is soft deletable
 */
export function isSoftDeletable(entity: any): entity is ISoftDeletable {
  return entity && typeof entity === 'object' && 'deletedAt' in entity
}


