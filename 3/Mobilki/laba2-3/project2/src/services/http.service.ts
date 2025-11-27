//npm install axios
//npm install --save-dev @types/axios 
//npm install --save-dev @types/node
import axios, { AxiosInstance, AxiosResponse } from 'axios';

class HttpService {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
    });
  }

  async get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get<T>(url, { params });
    return response.data;
  }
}

export const nobelApi = new HttpService('https://api.nobelprize.org/v1');