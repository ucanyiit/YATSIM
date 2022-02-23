import {
  Button, FormGroup, TextField, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../utils/RequestHandler';

const Login = ({ goHome }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div>
      <Typography variant="h4" component="h1" mt={2} mb={2}>
        Login
      </Typography>
      <form
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
        <FormGroup sx={{ mb: 2 }}>
          <TextField label="User Name" type="text" placeholder="User Name" onChange={(e) => setUsername(e.target.value)} required />
        </FormGroup>

        <FormGroup sx={{ mb: 2 }}>
          <TextField label="Password" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
        </FormGroup>

        {failed && (
        <p>
          Failed to login.
        </p>
        )}
        <Button size="large" loading={loading} disabled={loading} variant="contained" type="submit">
          Login
        </Button>
      </form>
    </div>
  );
};

export default Login;
