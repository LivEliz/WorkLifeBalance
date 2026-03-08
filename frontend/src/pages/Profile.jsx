import { deleteProfile, updateProfile } from "../services/api";

export default function Profile(){

  const handleDelete = async()=>{
    await deleteProfile();
    alert("Profile deleted");
  }

  return(

  <div className="page-container">

    <div className="form-card">

      <h2 className="page-title">Profile Settings</h2>

      <button onClick={updateProfile} className="primary-btn">
        Update Profile
      </button>

      <button onClick={handleDelete} className="danger-btn">
        Delete Profile
      </button>

    </div>

  </div>

  )
}