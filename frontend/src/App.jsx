import { useState, useEffect } from 'react'
import ContactList from './ContactList'
import ContactForm from './ContactForm'
import './App.css'

function App() {
  const [contacts, setContacts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentContact, setCurrentContact] = useState({})

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => {
    const response= await fetch("http://127.0.0.1:5000/contacts");
    if (!response.ok) {
      console.error("Failed to fetch contacts: ", response.statusText);
      return;
    }
    const data = await response.json();
    setContacts(data.contacts);
    console.log(data.contacts);
  };

const deleteContact = async (contactId) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/delete_contact/${contactId}`, { method: 'DELETE' });
    if (response.ok) {
      // If the delete was successful, filter out the deleted contact
      setContacts(contacts.filter(contact => contact.id !== contactId));
    } else {
      console.error('Failed to delete the contact');
    }
  } catch (error) {
    console.error('There was an error deleting the contact:', error);
  }
};

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (contact) => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  return (
    <>
      <ContactList contacts={contacts} updateContact={openEditModal} deleteContact={deleteContact} />
      <button id="addnew" onClick={openCreateModal}>Add New Contact Into Database</button>
      { isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
        </div>
      </div>
      }
    </>
  );
}

export default App
