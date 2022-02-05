export default class RequestHandler {
  headers;

  constructor() {
    this.headers = localStorage.getItem('token') ? { Authorization: `Token ${localStorage.getItem('token')}` } : {};
  }

  async request(endpoint, requestType, data = {}) {
    let response;
    const url = `http://localhost:8000/${endpoint}`;

    switch (requestType) {
      case 'get':
        response = await fetch(url, {
          method: 'GET',
          headers: this.headers,
        });
        break;
      case 'post':
        response = await fetch(url, {
          method: 'POST',
          body: data,
          headers: this.headers,
        });
        break;
      case 'put':
        response = await fetch(url, {
          method: 'PUT',
          body: data,
          headers: this.headers,
        });
        break;
      case 'delete':
        response = await fetch(url, {
          method: 'DELETE',
          body: data,
          headers: this.headers,
        });
        break;
      default:
        throw Error('Undefined requestType');
    }

    if (response.status >= 200 && response.status < 400) return (await response.json()).result;

    throw Error(response.data);
  }
}
