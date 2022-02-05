import { useState } from 'react';
import { Button } from 'react-bootstrap';

const Dashboard = ({ goRoom }) => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [data, setData] = useState(null);

  if (!loading && !failedToLoad && !data) {
    setLoading(true);
    fetch('http://localhost:8000/dashboard')
      .then((response) => {
        if (response.status >= 200 && response.status < 300 && response.data.response === 'success') setData(response.data.result);
        else setFailed(true);
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
      <ul>
        {data.owned_rooms.map((room) => (
          <li key={room.id}>
            {`${room.id}: `}
            <b>{room.owner__username}</b>
            {`/${room.room_name}, `}
            <Button onClick={() => goRoom(room.id)}>go</Button>
          </li>
        ))}
      </ul>

      <ul>
        {data.guest_rooms.map((room) => (
          <li key={room.id}>
            {`${room.id}: ${room.owner__username}/${room.room_name}, `}
            <Button onClick={() => goRoom(room.id)}>go</Button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
