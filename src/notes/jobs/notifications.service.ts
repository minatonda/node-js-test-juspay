import { InjectQueue } from "@nestjs/bullmq";
import { Queue } from "bullmq";
import { NoteEntity } from "../note.entity";

export class NotificationsService {
  constructor(@InjectQueue("notifications") private readonly queue: Queue) {}

  enqueueEmail(data: NoteEntity, schedule: string) {
    return this.queue.add("CREATED", data, {
      repeat: {
        pattern: getCronExpression(schedule),
        limit: 1,
      },
    });
  }

  async cancel(jobId: string): Promise<boolean> {
    const job = await this.queue.getJob(jobId);

    if (!job) {
      return false;
    }

    if (job.repeatJobKey) {
      await this.queue.removeRepeatableByKey(job.repeatJobKey);
    }

    await job.remove();
    return true;
  }
}

function getCronExpression(schedule: string) {
  const [hours, minutes] = schedule.split(":").map(Number);
  return `${minutes} ${hours} * * *`;
}
