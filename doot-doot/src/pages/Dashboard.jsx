import { useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [data, setData] = useState(null);

  if (!loading && !failedToLoad && !data) {
    setLoading(true);
    axios.get('http://localhost:8000/dashboard')
      .then((response) => {
        if (response.status === 200) setData(response.data);
        else setFailed(true);
      })
      .catch(() => setFailed(true))
      .finally(() => setLoading(false));
  }

  console.log(data);

  return (
    <div>
      Dashboard
      {/* <ol>
        {owned_rooms.map((room) => (
          <li>
            {`${room.id}: `}
            <b>{room.owner.username}</b>
            {`/${room.room_name}, `}
            <a href={room.id}>go</a>
          </li>
        ))}
      </ol>

      <ol>
        {guest_rooms.map((room) => (
          <li>
            {`${room.id}: ${room.owner.username}/${room.room_name}, `}
            <a href={room.id}>go</a>
          </li>
        ))}
      </ol> */}
    </div>
  );
};
export default Dashboard;
