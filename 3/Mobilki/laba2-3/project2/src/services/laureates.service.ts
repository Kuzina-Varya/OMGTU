import { nobelApi } from './http.service';

export interface NobelLaureate {
  id: string;
  firstname?: string;
  surname?: string;
  born?: string;
  died?: string;
  gender: string;
  prizes: Array<{
    year: string;
    category: string;
  }>;
}

export interface LaureateResponse {
  laureates: NobelLaureate[];
}

export class LaureatesService {
  static async getAll(page = 1, limit = 10): Promise<NobelLaureate[]> {
    const data = await nobelApi.get<LaureateResponse>('/laureate.json');
    // Nobel API не поддерживает пагинацию → делаем её на клиенте
    const startIndex = (page - 1) * limit;
    return data.laureates.slice(startIndex, startIndex + limit);
  }

  static async searchByName(name: string): Promise<NobelLaureate[]> {
    const data = await nobelApi.get<LaureateResponse>('/laureate.json');
    const query = name.toLowerCase();
    return data.laureates.filter(l => {
      const fullName = `${l.firstname || ''} ${l.surname || ''}`.toLowerCase();
      return fullName.includes(query);
    });
  }
}