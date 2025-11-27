import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  HttpStatus,
  Param,
  Patch,
  Post,
  Query,
  ParseUUIDPipe,
} from "@nestjs/common";
import {
  ApiOperation,
  ApiResponse,
  ApiTags,
  ApiParam,
  ApiQuery,
} from "@nestjs/swagger";
import { NotesService } from "./notes.service";
import { CreateNoteDto } from "./dto/create-note.dto";
import { UpdateNoteDto } from "./dto/update-note.dto";
import { ListNotesQueryDto } from "./dto/list-notes-query.dto";
import { ListNotesResponseDto } from "./dto/list-notes-response.dto";
import { NoteEntity } from "./note.entity";
import { createUuidValidationPipe } from "../common/pipes/uuid-validation.pipe";
import { UpdateNotificationScheduleDto } from "./dto/update-notification-schedule.dto";

@ApiTags("Notes")
@Controller("notes")
export class NotesController {
  constructor(private readonly notesService: NotesService) {}

  @Post()
  @ApiOperation({ summary: "Create a new note" })
  @ApiResponse({
    status: 201,
    description: "Note created successfully",
    type: NoteEntity,
  })
  @ApiResponse({ status: 400, description: "Invalid data" })
  async create(
    @Body() dto: CreateNoteDto,
    @Query("notification-schedule") schedule: string
  ): Promise<NoteEntity> {
    return this.notesService.create(dto, { schedule });
  }

  @Get()
  @ApiOperation({ summary: "List notes with pagination, search and filters" })
  @ApiResponse({
    status: 200,
    description: "List of notes returned successfully",
    type: ListNotesResponseDto,
  })
  async findAll(
    @Query() query: ListNotesQueryDto
  ): Promise<ListNotesResponseDto> {
    return this.notesService.findAll(query);
  }

  @Get(":id")
  @ApiOperation({ summary: "Find a note by ID" })
  @ApiParam({ name: "id", description: "Note UUID", type: String })
  @ApiResponse({ status: 200, description: "Note found", type: NoteEntity })
  @ApiResponse({ status: 404, description: "Note not found" })
  async findOne(
    @Param("id", createUuidValidationPipe("Note")) id: string
  ): Promise<NoteEntity> {
    return this.notesService.findOne(id);
  }

  @Patch(":id/notification-schedule")
  @ApiOperation({ summary: "Reschedule a note notification" })
  @ApiParam({ name: "id", description: "Note UUID", type: String })
  @ApiResponse({
    status: 200,
    description: "Notification schedule updated successfully",
  })
  @ApiResponse({ status: 404, description: "Note not found" })
  @ApiResponse({ status: 400, description: "Invalid data" })
  async updateNotificationSchedule(
    @Param("id", new ParseUUIDPipe({ version: "4" })) id: string,
    @Body() dto: UpdateNotificationScheduleDto
  ) {
    const jobId = await this.notesService.rescheduleNotification(
      id,
      dto.schedule
    );

    return {
      message: "Notification schedule updated",
      jobId,
      schedule: dto.schedule,
    };
  }

  @Patch(":id")
  @ApiOperation({ summary: "Update a note (partial or complete)" })
  @ApiParam({ name: "id", description: "Note UUID", type: String })
  @ApiResponse({
    status: 200,
    description: "Note updated successfully",
    type: NoteEntity,
  })
  @ApiResponse({ status: 404, description: "Note not found" })
  @ApiResponse({ status: 400, description: "Invalid data" })
  async update(
    @Param("id", new ParseUUIDPipe({ version: "4" })) id: string,
    @Body() dto: UpdateNoteDto
  ): Promise<NoteEntity> {
    return this.notesService.update(id, dto);
  }

  @Delete(":id")
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Delete a note (soft delete)" })
  @ApiParam({ name: "id", description: "Note UUID", type: String })
  @ApiResponse({ status: 200, description: "Note deleted successfully" })
  @ApiResponse({ status: 404, description: "Note not found" })
  async remove(@Param("id", new ParseUUIDPipe({ version: "4" })) id: string) {
    await this.notesService.remove(id);
    return { message: "Note deleted successfully" };
  }
}
