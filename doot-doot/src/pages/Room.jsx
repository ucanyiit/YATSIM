import { useState } from 'react';
import axios from 'axios';

const Room = ({ id }) => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [data, setData] = useState(null);

  if (!loading && !failedToLoad && !data) {
    setLoading(true);
    axios.get('http://localhost:8000/dashboard')
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
      room room
      {' '}
      {id}
    </div>
  );
};

export default Room;
