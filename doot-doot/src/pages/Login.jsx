import { useState } from 'react';
import axios from 'axios';
import { Button, Form } from 'react-bootstrap';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  if (loading || failedToLoad) {
    return (
      <div>
        {failedToLoad && 'Failed to load'}
        {loading && 'Loading..'}
      </div>
    );
  }

  return (
    <div>
      <h2>
        Login
      </h2>
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          console.log(password, username);
          setLoading(true);
          axios.get('http://localhost:8000/dashboard')
            .then((response) => {
              console.log('yes', response);
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

        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
};

export default Login;
