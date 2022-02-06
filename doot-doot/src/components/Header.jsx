import { Button } from 'react-bootstrap';

const Header = ({ setPage, token }) => (
  <div className="mb-3">
    <Button className="me-2" onClick={() => setPage('home')}>
      Home
    </Button>
    {token && (
    <Button className="me-2" onClick={() => setPage('create')}>
      Create Room
    </Button>
    )}
    {!token && (
    <Button onClick={() => setPage('login')}>
      Login
    </Button>
    )}
    {token && (
      <Button onClick={() => {
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
