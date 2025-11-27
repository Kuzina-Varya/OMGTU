import { nobelApi } from './http.service';

export interface NobelPrize {
  year: string;
  category: string;
  laureates?: Array<{
    id: string;
    firstname?: string;
    surname?: string;
  }>;
}

export interface PrizeResponse {
  prizes: NobelPrize[];
}

export class PrizesService {
  static async getAll(page = 1, limit = 10): Promise<NobelPrize[]> {
    const data = await nobelApi.get<PrizeResponse>('/prize.json');
    const startIndex = (page - 1) * limit;
    return data.prizes.slice(startIndex, startIndex + limit);
  }

  static async searchByCategory(category: string): Promise<NobelPrize[]> {
    const data = await nobelApi.get<PrizeResponse>('/prize.json');
    const query = category.toLowerCase();
    return data.prizes.filter(p => p.category.toLowerCase().includes(query));
  }
}