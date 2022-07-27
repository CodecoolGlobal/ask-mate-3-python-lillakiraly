const openProfileButton = document.querySelector('#open')
const userProfile = document.querySelector('#profile_container')
const closeProfileButton = document.querySelector('#close')

openProfileButton.addEventListener('click', () => {
    console.log('Profile opened')
    userProfile.classList.add('show');
});

closeProfileButton.addEventListener('click', () => {
    console.log('Profile closed')
    userProfile.classList.remove('show')
});