import { Button } from '@mui/material';

const Header = ({ setPage, token }) => (
  <div sx={{ mb: 2 }}>
    <Button variant="contained" sx={{ mr: 1 }} onClick={() => setPage('home')}>
      Home
    </Button>
    {token && (
    <Button variant="contained" sx={{ mr: 1 }} onClick={() => setPage('create')}>
      Create Room
    </Button>
    )}
    {!token && (
    <Button variant="contained" onClick={() => setPage('login')}>
      Login
    </Button>
    )}
    {token && (
      <Button
        variant="contained"
        onClick={() => {
          localStorage.removeItem('token');
          window.location.reload(false);
        }}
      >
        Logout
      </Button>
    )}
  </div>
);

export default Header;
