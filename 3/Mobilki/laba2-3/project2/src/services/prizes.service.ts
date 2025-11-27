// src/services/prizes.service.ts
import { nobelApi } from './http.service';
import {
  PrizesResponseCodec,
  PrizesResponse,
  NobelPrize
} from '@/types/nobel.types';

export class PrizesService {
  static async getAll(page = 1, limit = 10): Promise<NobelPrize[]> {
    const data: PrizesResponse = await nobelApi.get('/prize.json', PrizesResponseCodec);
    const startIndex = (page - 1) * limit;
    return data.prizes.slice(startIndex, startIndex + limit);
  }

  static async searchByCategory(category: string): Promise<NobelPrize[]> {
    const data: PrizesResponse = await nobelApi.get('/prize.json', PrizesResponseCodec);
    const query = category.toLowerCase();
    return data.prizes.filter((p: NobelPrize) =>
      p.category.toLowerCase().includes(query)
    );
  }
}