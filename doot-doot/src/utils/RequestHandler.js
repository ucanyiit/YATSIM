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
          body: JSON.stringify(data),
          headers: { ...this.headers, 'Content-Type': 'application/json' },
        });
        break;
      case 'put':
        response = await fetch(url, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers: { ...this.headers, 'Content-Type': 'application/json' },
        });
        break;
      case 'delete':
        response = await fetch(url, {
          method: 'DELETE',
          body: JSON.stringify(data),
          headers: { ...this.headers, 'Content-Type': 'application/json' },
        });
        break;
      default:
        throw Error('Undefined requestType');
    }

    if (response.status >= 200 && response.status < 400) return response.json();

    throw Error(response.data);
  }
}
