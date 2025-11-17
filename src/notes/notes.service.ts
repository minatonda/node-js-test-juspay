import { Injectable, Logger, NotFoundException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
import { Repository } from 'typeorm'
import { NoteEntity } from './note.entity'
import { CreateNoteDto } from './dto/create-note.dto'
import { UpdateNoteDto } from './dto/update-note.dto'
import { ListNotesQueryDto, SortBy, SortOrder } from './dto/list-notes-query.dto'
import { ListNotesResponseDto } from './dto/list-notes-response.dto'
import { normalizePaginationParams, createPaginationResponse } from '../common/utils/pagination.util'
import { applySoftDeleteFilter, excludeDeleted, performSoftDelete } from '../common/utils/soft-delete.util'

@Injectable()
export class NotesService {
  private readonly logger = new Logger(NotesService.name)

  constructor(
    @InjectRepository(NoteEntity)
    private readonly repository: Repository<NoteEntity>,
  ) {}

  async create(dto: CreateNoteDto): Promise<NoteEntity> {
    this.logger.log(`Creating note with title: ${dto.title}, tags: ${JSON.stringify(dto.tags)}`)

    // Ensure tags is always an array (the hook also ensures this, but we do it here too)
    const tags = Array.isArray(dto.tags) ? dto.tags : []

    const note = this.repository.create({
      title: dto.title,
      body: dto.body,
      tags: tags,
    })

    const saved = await this.repository.save(note)
    this.logger.log(`Note created successfully with id: ${saved.id}, tags: ${JSON.stringify(saved.tags)}, type: ${typeof saved.tags}, isArray: ${Array.isArray(saved.tags)}`)

    // Check what's actually in the database
    const rawNote = await this.repository
      .createQueryBuilder('note')
      .where('note.id = :id', { id: saved.id })
      .getRawOne()
    if (rawNote) {
      this.logger.log(`Raw tags from DB (note_tags): ${rawNote.note_tags}, type: ${typeof rawNote.note_tags}`)
    }

    return saved
  }

  async findAll(query: ListNotesQueryDto): Promise<ListNotesResponseDto> {
    const { search, tags, sortBy = SortBy.CREATED_AT, sortOrder = SortOrder.DESC } = query

    // Normalize pagination parameters
    const { page, limit } = normalizePaginationParams(query.page, query.limit)

    this.logger.log(`Finding notes - page: ${page}, limit: ${limit}, search: ${search || 'none'}, tags: ${tags?.join(',') || 'none'}`)

    const queryBuilder = this.repository.createQueryBuilder('note')

    // Soft delete: only non-deleted notes
    applySoftDeleteFilter(queryBuilder, 'note')

    // Search by keywords (title or body)
    if (search) {
      queryBuilder.andWhere(
        '(LOWER(note.title) LIKE LOWER(:search) OR LOWER(note.body) LIKE LOWER(:search))',
        { search: `%${search}%` },
      )
    }

    // Filter by tags: check if the note's tag array has intersection with the provided tags
    if (tags && tags.length > 0) {
      // SQLite: use json_each to search within the JSON array
      const tagsPlaceholders = tags.map((_, index) => `:tag${index}`).join(', ')
      const tagsParams: Record<string, string> = {}
      tags.forEach((tag, index) => {
        tagsParams[`tag${index}`] = String(tag)
      })
      queryBuilder.andWhere(
        `EXISTS (
          SELECT 1 FROM json_each(note.tags) 
          WHERE json_each.value IN (${tagsPlaceholders})
        )`,
        tagsParams,
      )
    }

    // Sorting
    const orderByField = sortBy === SortBy.CREATED_AT ? 'note.createdAt' : sortBy === SortBy.UPDATED_AT ? 'note.updatedAt' : 'note.title'
    queryBuilder.orderBy(orderByField, sortOrder)

    // Pagination
    queryBuilder.skip((page - 1) * limit)
    queryBuilder.take(limit)

    const [items, total] = await queryBuilder.getManyAndCount()

    this.logger.log(`Found ${items.length} notes out of ${total} total`)

    // Use pagination utility to create consistent response
    const paginationResult = createPaginationResponse(items, total, page, limit)
    
    // Return as ListNotesResponseDto (compatible structure)
    return {
      items: paginationResult.items,
      total: paginationResult.total,
      page: paginationResult.page,
      limit: paginationResult.limit,
      pageCount: paginationResult.pageCount,
    } as ListNotesResponseDto
  }

  async findOne(id: string): Promise<NoteEntity> {
    this.logger.log(`Finding note with id: ${id}`)

    const note = await this.repository.findOne({
      where: excludeDeleted({ id }),
    })

    if (!note) {
      this.logger.warn(`Note not found with id: ${id} (may be deleted)`)
      throw new NotFoundException('Note not found')
    }

    return note
  }

  async update(id: string, dto: UpdateNoteDto): Promise<NoteEntity> {
    this.logger.log(`Updating note with id: ${id}`)

    const note = await this.findOne(id)

    if (dto.title !== undefined) {
      note.title = dto.title
    }
    if (dto.body !== undefined) {
      note.body = dto.body
    }
    if (dto.tags !== undefined) {
      note.tags = dto.tags
    }

    const updated = await this.repository.save(note)
    this.logger.log(`Note updated successfully with id: ${updated.id}`)

    return updated
  }

  async remove(id: string): Promise<void> {
    this.logger.log(`Deleting note with id: ${id}`)

    const note = await this.findOne(id)

    // Soft delete
    performSoftDelete(note)
    await this.repository.save(note)

    this.logger.log(`Note deleted successfully with id: ${id}`)
  }

  async search(keyword: string, page: number = 1, limit: number = 20) {
    this.logger.log(`Searching notes with keyword: ${keyword}`)

    return this.findAll({
      search: keyword,
      page,
      limit,
    })
  }
}

