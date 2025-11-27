import { ApiProperty } from "@nestjs/swagger";
import { IsString, Matches } from "class-validator";

export class UpdateNotificationScheduleDto {
  @ApiProperty({
    description: "Horário no formato HH:mm",
    example: "13:30",
  })
  @IsString()
  @Matches(/^\d{2}:\d{2}$/, {
    message: "schedule must follow the HH:mm format",
  })
  schedule: string;
}

