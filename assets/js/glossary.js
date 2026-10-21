// Opens the translator's notes when the homepage is reached via #glossary (the post-page footer links here).
if (location.hash === '#glossary') {
  const notes = document.getElementById('glossary');
  if (notes && notes.showPopover) notes.showPopover();
}
