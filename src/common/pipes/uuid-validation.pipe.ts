import { PipeTransform, Injectable, NotFoundException, ArgumentMetadata } from '@nestjs/common'
import { isValidUUID } from '../utils/uuid.util'

/**
 * Custom pipe that validates UUID and throws NotFoundException (404) instead of BadRequestException (400)
 * This provides better UX by treating invalid UUIDs as "not found" rather than "bad request"
 */
@Injectable()
export class UuidValidationPipe implements PipeTransform<string, string> {
  constructor(private readonly entityName: string = 'Entity') {}

  transform(value: string, metadata: ArgumentMetadata): string {
    if (!isValidUUID(value)) {
      throw new NotFoundException(`${this.entityName} not found`)
    }
    return value
  }
}

/**
 * Factory function to create UUID validation pipe with entity name
 * @param entityName - Name of the entity (e.g., 'Note', 'User')
 * @returns UuidValidationPipe instance
 */
export function createUuidValidationPipe(entityName: string): UuidValidationPipe {
  return new UuidValidationPipe(entityName)
}


