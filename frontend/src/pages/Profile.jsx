import { deleteProfile, updateProfile } from "../services/api";

export default function Profile(){

  const handleDelete = async()=>{
    await deleteProfile();
    alert("Profile deleted");
  }

  return(
    <div>

      <h2>Profile Settings</h2>

      <button onClick={updateProfile}>
        Update Profile
      </button>

      <button onClick={handleDelete}>
        Delete Profile
      </button>

    </div>
  )
}