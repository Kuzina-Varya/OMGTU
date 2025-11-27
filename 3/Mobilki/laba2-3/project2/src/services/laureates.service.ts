// src/services/laureates.service.ts
import { nobelApi } from './http.service';
import {
  LaureatesResponseCodec,
  LaureatesResponse,
  NobelLaureate
} from '@/types/nobel.types';

export class LaureatesService {
  static async getAll(page = 1, limit = 10): Promise<NobelLaureate[]> {
    const data: LaureatesResponse = await nobelApi.get('/laureate.json', LaureatesResponseCodec);
    const startIndex = (page - 1) * limit;
    return data.laureates.slice(startIndex, startIndex + limit);
  }

  static async searchByName(name: string): Promise<NobelLaureate[]> {
    const data: LaureatesResponse = await nobelApi.get('/laureate.json', LaureatesResponseCodec);
    const query = name.toLowerCase();
    return data.laureates.filter((l: NobelLaureate) =>
      `${l.firstname || ''} ${l.surname || ''}`.toLowerCase().includes(query)
    );
  }
}