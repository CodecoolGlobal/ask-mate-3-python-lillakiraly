const openProfileButtons = document.querySelectorAll('#open')
const userProfile = document.querySelector('.profile-container')
const closeProfileButton = document.querySelector('#close')

for (const element of openProfileButtons) {
    element.addEventListener('click', () => {
        userProfile.classList.add('show')
        let profile = userProfile.firstChild.nextSibling
        profile.setAttribute('id', element.textContent)
        profile.firstElementChild.textContent = element.textContent
        console.log('Profile opened');
    });
}

closeProfileButton.addEventListener('click', () => {
    userProfile.classList.remove('show')
    console.log('Profile closed');
});