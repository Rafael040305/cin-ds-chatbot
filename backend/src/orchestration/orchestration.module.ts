import { Module } from '@nestjs/common';
import { AiServiceModule } from '../ai-service/ai-service.module.js';
import {
  FALLBACK_DISTANCE_THRESHOLD,
  readFallbackDistanceThreshold,
} from './fallback.config.js';
import { FallbackService } from './fallback.service.js';
import { OrchestrationService } from './orchestration.service.js';

@Module({
  imports: [AiServiceModule],
  providers: [
    {
      provide: FALLBACK_DISTANCE_THRESHOLD,
      useFactory: readFallbackDistanceThreshold,
    },
    FallbackService,
    OrchestrationService,
  ],
  exports: [OrchestrationService],
})
export class OrchestrationModule {}
