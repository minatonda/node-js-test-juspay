import { BullModule } from "@nestjs/bullmq";
import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { NotificationsProcessor } from "./jobs/notifications.processor";
import { NOTIFICATIONS_QUEUE_OPTIONS } from "./jobs/notifications.queue-options";
import { NotificationsService } from "./jobs/notifications.service";
import { NoteEntity } from "./note.entity";
import { NotesController } from "./notes.controller";
import { NotesService } from "./notes.service";

@Module({
  imports: [
    TypeOrmModule.forFeature([NoteEntity]),
    BullModule.registerQueue(NOTIFICATIONS_QUEUE_OPTIONS),
  ],
  controllers: [NotesController],
  providers: [NotesService, NotificationsService, NotificationsProcessor],
  exports: [NotesService],
})
export class NotesModule {}
