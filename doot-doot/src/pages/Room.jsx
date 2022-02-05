import { useState } from 'react';
import RequestHandler from '../utils/RequestHandler';

const Room = ({ id }) => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [data, setData] = useState(null);

  if (!loading && !failedToLoad && !data) {
    setLoading(true);
    (new RequestHandler()).request(`room/${id}`, 'get')
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
      room room
      {' '}
      {id}
    </div>
  );
};

export default Room;
