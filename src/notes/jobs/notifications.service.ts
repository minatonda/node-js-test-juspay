import { InjectQueue } from "@nestjs/bullmq";
import { Queue } from "bullmq";
import { NoteEntity } from "../note.entity";

export class NotificationsService {
  constructor(@InjectQueue("notifications") private readonly queue: Queue) {}

  enqueueEmail(data: NoteEntity, schedulle: string) {
    return this.queue.add("CREATED", data, {
      repeat: {
        pattern: getCronExpression(schedulle),
        limit: 1,
      },
    });
  }
}

function getCronExpression(schedule: string) {
  const [hours, minutes] = schedule.split(":").map(Number);
  return `${minutes} ${hours} * * *`;
}
