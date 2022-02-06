import { useState } from 'react';

const Room = ({ roomData: { room, cells, trains } }) => {
  const running = false;
  const [grid, setMap] = useState(null);

  const newGrid = [];
  const newCells = cells.sort((a, b) => {
    if (a.y < b.y) return -1;
    if (a.y > b.y) return 1;
    return a.x < b.x ? -1 : 1;
  });
  // eslint-disable-next-line no-restricted-syntax
  for (let i = 0; i < room.height; i += 1) {
    const row = [];
    for (let j = 0; j < room.width; j += 1) {
      row.push(newCells[i * room.width + j]);
    }
    newGrid.push(row);
  }

  if (JSON.stringify(grid) !== JSON.stringify(newGrid)) {
    setMap(newGrid);
  }

  if (!grid) {
    return (
      <div>
        Loading...
      </div>
    );
  }

  console.log(room, cells, trains, grid);
  return (
    <div>
      <h5>
        {`${room.id}: `}
        <b>{room.owner.username}</b>
        {`/${room.room_name}, height: ${room.height}, width: ${room.width}, ${running && 'Simulation is running 🚀'}${!running && 'Simulation is stopped 🌱'}`}
      </h5>
      <div>
        Guests:
        {room.guests.map((u) => (
          <span>
            {u.username}
          </span>
        ))}
      </div>
      <center>
        <table>
          {grid.map((row) => (
            <tr>
              {row.map((cell) => (
                <td>
                  <div className="cell">
                    {cell.direction}

                  </div>
                </td>
              ))}
            </tr>
          ))}
        </table>
      </center>

    </div>
  );
};

export default Room;
