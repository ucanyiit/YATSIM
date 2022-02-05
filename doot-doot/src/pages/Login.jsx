import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../utils/RequestHandler';

const Login = ({ goHome }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div>
      <h2>
        Login
      </h2>
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request('api/auth/login/', 'post', { password, username })
            .then((response) => {
              localStorage.setItem('token', response.token);
              goHome();
            })
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="name">
          <Form.Label>User Name</Form.Label>
          <Form.Control type="text" placeholder="User Name" onChange={(e) => setUsername(e.target.value)} required />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Width</Form.Label>
          <Form.Control type="password" placeholder="Passowrd" onChange={(e) => setPassword(e.target.value)} required />
        </Form.Group>

        {failed && (
        <p>
          Failed to login.
        </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
};

export default Login;
