import { useState } from 'react';
import { Button, ListGroup } from 'react-bootstrap';
import RequestHandler from '../utils/RequestHandler';

const Dashboard = ({ goRoom }) => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [data, setData] = useState(null);

  if (!loading && !failedToLoad && !data) {
    setLoading(true);
    (new RequestHandler()).request('dashboard', 'get')
      .then((response) => {
        setData(response);
      })
      .catch(() => setFailed(true))
      .finally(() => setLoading(false));
  }

  if (loading || !data || failedToLoad) {
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
        Home
      </h2>
      <span>
        {`You are logged in as ${data.user.username}.`}
      </span>
      <ListGroup>
        {data.owned_rooms.map((room) => (
          <ListGroup.Item key={room.id}>
            {`${room.id}: `}
            <b>{room.owner.username}</b>
            {`/${room.room_name}, `}
            <Button onClick={() => goRoom(room.id)}>go</Button>
          </ListGroup.Item>
        ))}
      </ListGroup>

      <ListGroup>
        {data.guest_rooms.map((room) => (
          <ListGroup.Item key={room.id}>
            {`${room.id}: ${room.owner.username}/${room.room_name}, `}
            <Button onClick={() => goRoom(room.id)}>go</Button>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
};

export default Dashboard;
