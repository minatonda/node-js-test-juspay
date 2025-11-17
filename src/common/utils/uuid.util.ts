/**
 * UUID utility functions
 * Provides consistent UUID validation across the application
 */

/**
 * UUID v4 validation regex pattern
 */
export const UUID_V4_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

/**
 * Validates if a string is a valid UUID v4
 * @param value - String to validate
 * @returns true if valid UUID v4, false otherwise
 */
export function isValidUUID(value: string): boolean {
  if (!value || typeof value !== 'string') {
    return false
  }
  return UUID_V4_REGEX.test(value)
}

/**
 * Validates UUID and throws NotFoundException if invalid
 * This provides better UX by returning 404 instead of 400 for invalid UUIDs
 * @param value - String to validate
 * @param entityName - Name of the entity (e.g., 'Note', 'User')
 * @throws NotFoundException if UUID is invalid
 */
export function validateUUIDOrThrow(value: string, entityName: string = 'Entity'): void {
  if (!isValidUUID(value)) {
    const { NotFoundException } = require('@nestjs/common')
    throw new NotFoundException(`${entityName} not found`)
  }
}


