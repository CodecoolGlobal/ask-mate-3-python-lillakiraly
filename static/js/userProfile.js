const openProfileButton = document.querySelector('#open')
const userProfile = document.querySelector('.profile-container')
const closeProfileButton = document.querySelector('#close')

openProfileButton.addEventListener('click', () => {
    userProfile.classList.add('show')
    console.log('Profile opened');
    console.log(userProfile)
});

closeProfileButton.addEventListener('click', () => {
    userProfile.classList.remove('show')
    console.log('Profile closed');
    console.log(userProfile)
});