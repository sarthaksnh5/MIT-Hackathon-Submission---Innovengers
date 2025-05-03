import {useState} from 'react';
import axios, {AxiosRequestConfig, Method} from 'axios';
import {useNavigation} from '@react-navigation/native';
import {useAuthStore} from '../store/useAuthStore';
import {showGlobalSnackbar} from './useSnackbar';

type HttpMethod = Method;
type Status = 'idle' | 'loading' | 'success' | 'error';

type RequestOptions = {
  requireAuth?: boolean;
  showSnackbar?: boolean;
  successMessage?: string;
  errorMessage?: string;
  headers?: Record<string, string>;
  queryParams?: Record<string, string | number | boolean>;
};

type ApiResponse<T> = {
  data: T | null;
  error: string | null;
  loading: boolean;
  status: Status;
  request: (
    endpoint: string,
    method?: HttpMethod,
    body?: any,
    options?: RequestOptions,
  ) => Promise<{data: T | null; error: string | null; status: Status}>;
};

export function useApi<T = any>(): ApiResponse<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>('idle');

  const {accessToken, logout} = useAuthStore();
  const navigation = useNavigation<any>();

  const request = async (
    endpoint: string,
    method: HttpMethod = 'GET',
    body?: any,
    options: RequestOptions = {},
  ): Promise<{data: T | null; error: string | null; status: Status}> => {
    const {
      requireAuth = true,
      showSnackbar: shouldShowSnackbar = true,
      successMessage,
      errorMessage,
      headers: extraHeaders = {},
      queryParams = {},
    } = options;

    setStatus('loading');
    setError(null);
    setData(null);

    if (shouldShowSnackbar) {
      showGlobalSnackbar('Loading...', 'gray');
    }

    try {
      const headers: Record<string, string> = {
        'Content-Type': extraHeaders['Content-Type'] || 'application/json',
        ...extraHeaders,
      };

      if (requireAuth && accessToken) {
        headers.Authorization = `Bearer ${accessToken}`;
      }

      const params = {...queryParams};

      const config: AxiosRequestConfig = {
        url: endpoint,
        method,
        headers,
        params,
        data: ['POST', 'PUT', 'PATCH'].includes(method) ? body : undefined,
      };

      const response = await axios(config);

      setData(response.data);
      setStatus('success');

      if (shouldShowSnackbar) {
        showGlobalSnackbar(successMessage || 'Request successful', 'green');
      }

      return {data: response.data, error: null, status: 'success'};
    } catch (err: any) {
      const res = err.response;

      let errMsg = errorMessage || err.message || 'Network error';

      if (res?.data && typeof res.data === 'object') {
        const json = res.data;
        const firstField = Object.keys(json)[0];
        if (firstField && typeof json[firstField] === 'string') {
          errMsg = json[firstField];
        } else if (firstField && Array.isArray(json[firstField])) {
          errMsg = json[firstField][0];
        } else if (json.detail) {
          errMsg = json.detail;
        }
      }

      if (res?.status === 401) {
        logout();
        if (shouldShowSnackbar) {
          showGlobalSnackbar('Login expired, please login again.', 'red');
        }
        navigation.reset({
          index: 0,
          routes: [{name: 'Login'}],
        });
      } else if (shouldShowSnackbar) {
        showGlobalSnackbar(errMsg, 'red');
      }

      setError(errMsg);
      setStatus('error');
      return {data: null, error: errMsg, status: 'error'};
    }
  };

  return {
    data,
    error,
    loading: status === 'loading',
    status,
    request,
  };
}
