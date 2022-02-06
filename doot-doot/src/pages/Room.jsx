const Room = ({ roomData: { room, running } }) => (
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

  </div>
);

export default Room;
