const noteList = document.querySelector('.note-list');
const createNoteBtn = document.getElementById("create-note");
const editNoteBtn = document.getElementById('edit-note');
const saveNoteBtn = document.getElementById('save-note');
const deleteNoteBtn = document.getElementById('delete-note');
const noteContent = document.getElementById('note-content');
const noteTitle = document.getElementById('note-title');
const navigation = document.getElementById('navigation');
const hideButton = document.getElementById('hide-button');
const menuButton = document.getElementById('menu-button');
const main_page = document.getElementsByClassName("content")

// Event listener for menu button click to toggle navigation visibility
menuButton.addEventListener('click', () => {
  navigation.classList.toggle('active'); 
  navigation.classList.remove("hidden");// Use 'active' class
});

// Event listener for hide button click
hideButton.addEventListener('click', () => {
  navigation.classList.toggle('hidden'); 
  navigation.classList.remove('active');// Use 'hidden' class for opacity
});