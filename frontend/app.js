const API = 'http://127.0.0.1:8000';

let step = 1,
    theme = 'iconic_call',
    intensity = 'crazy',
    html = '';

let experienceId = null;
let previewUrl = null;
let downloadUrl = null;

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

function goForm() {
    $('#builder').scrollIntoView({ behavior: 'smooth' });
}

function chips(text, cls) {
    return text
        .split('|')
        .map(x => `<button type="button">${x}</button>`)
        .join('');
}

$$('.chips').forEach(x => {
    x.innerHTML = chips(x.textContent.trim());
});

$$('.chips button').forEach(b => {
    b.onclick = () => b.classList.toggle('selected');
});

const THEMES = [
    {
        value: 'iconic_call',
        icon: '📞',
        title: 'The Call',
        description: 'A surprise call from someone they admire',
        featured: true
    },
    {
        value: 'cricket',
        icon: '🏏',
        title: 'Cricket Legend',
        description: 'Stadium energy, stats and birthday banter'
    },
    {
        value: 'mystery',
        icon: '🕵️',
        title: 'Classified Mystery',
        description: 'A suspense thriller birthday story'
    },
    {
        value: 'cinema',
        icon: '🎬',
        title: 'Movie Trailer',
        description: 'Their life becomes the next blockbuster'
    },
    {
        value: 'gaming',
        icon: '🎮',
        title: 'Game Mode',
        description: 'Levels, achievements and boss fights'
    },
    {
        value: 'emotional',
        icon: '❤️',
        title: 'Heartfelt',
        description: 'A beautiful friendship story'
    },
    {
        value: 'surprise',
        icon: '✨',
        title: 'Surprise Me',
        description: 'Let AI choose the experience'
    }
];


$('.themes').innerHTML = THEMES
    .map((t, i) => `
        <button
            type="button"
            data-v="${t.value}"
            class="${i === 0 ? 'selected featured-theme' : ''}"
        >
            <span class="theme-icon">${t.icon}</span>

            <strong>${t.title}</strong>

            <small>${t.description}</small>

            ${
                t.featured
                    ? '<b class="theme-badge">SIGNATURE</b>'
                    : ''
            }
        </button>
    `)
    .join('');


$$('.themes button').forEach(b => {

    b.onclick = () => {

        $$('.themes button')
            .forEach(x =>
                x.classList.remove('selected')
            );

        b.classList.add('selected');

        theme = b.dataset.v;

    };

});

$('.levels').innerHTML = 'Simple|Creative|Crazy 🔥|Absolutely Insane 🤯'
    .split('|')
    .map((x, i) =>
        `<button type="button"
            class="${i === 2 ? 'selected' : ''}"
            data-v="${['simple', 'creative', 'crazy', 'insane'][i]}">
            ${x}
        </button>`
    )
    .join('');

$$('.levels button').forEach(b => {
    b.onclick = () => {
        $$('.levels button').forEach(x => x.classList.remove('selected'));
        b.classList.add('selected');
        intensity = b.dataset.v;
    };
});

function show(n) {
    step = n;

    $$('.step').forEach(x =>
        x.classList.toggle('active', +x.dataset.step === n)
    );

    $('#back').style.visibility = n === 1 ? 'hidden' : 'visible';

    $('#next').textContent =
        n === 4
            ? 'Create their experience ✦'
            : 'Continue →';

    $('#count').textContent = `${n} / 4`;

    document.querySelector('#bar').style.width = n * 25 + '%';
}

function data() {
    let f = new FormData($('#form'));

    let get = g =>
        $$(`.chips[data-name="${g}"] button.selected`)
            .map(x => x.textContent.trim());

    return {
        name: f.get('name'),
        age: f.get('age') ? +f.get('age') : null,
        gender: f.get('gender'),
        location: f.get('location'),
        relationship: f.get('relationship'),
        known_since: f.get('known_since'),
        how_met: f.get('how_met'),
        personality: get('personality'),
        interests: get('interests'),
        favorite_person: f.get('favorite_person'),
        favorite_movie_genre: f.get('favorite_movie_genre'),
        memorable_story: f.get('memorable_story'),
        funny_fact: f.get('funny_fact'),
        achievement: f.get('achievement'),
        private_note: f.get('private_note'),
        birthday_message: f.get('birthday_message'),
        theme,
        intensity
    };
}

async function generate() {

    const p = data();

    if (!p.name) {

        alert(
            'Please enter their name.'
        );

        return;
    }


    $('#form').style.display = 'none';

    $('.heading').style.display = 'none';

    $('.builder>label').style.display =
        'none';

    $('#generating')
        .classList
        .add('active');


    try {

        const response = await fetch(
            API + '/api/birthday/generate',
            {
                method: 'POST',

                headers: {
                    'Content-Type':
                        'application/json'
                },

                body: JSON.stringify(p)
            }
        );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        const result =
            await response.json();


        experienceId =
            result.experience_id;


        previewUrl =
            API + result.preview_url;


        downloadUrl =
            API + result.download_url;


        /*
         * Show result screen.
         */

        setTimeout(() => {

            $('#generating')
                .classList
                .remove('active');

            $('#result')
                .classList
                .add('active');

        }, 1100);


    } catch (error) {

        console.error(
            'Generation failed:',
            error
        );


        $('#form').style.display = '';

        $('.heading').style.display = '';

        $('.builder>label').style.display =
            '';


        $('#generating')
            .classList
            .remove('active');


        alert(
            'Something went wrong while creating the experience.'
        );
    }
}

$('#next').onclick = () =>
    step < 4
        ? show(step + 1)
        : generate();

$('#back').onclick = () =>
    step > 1 && show(step - 1);

$('#open').onclick = () => {

    if (!previewUrl) {
        return;
    }

    window.open(
        previewUrl,
        '_blank'
    );

};

$('#download').onclick = () => {

    if (!downloadUrl) {
        return;
    }

    const link =
        document.createElement('a');

    link.href = downloadUrl;

    link.download = '';

    document.body.appendChild(link);

    link.click();

    link.remove();

};

$('#copyLink').onclick =
    async () => {

        if (!previewUrl) {
            return;
        }


        /*
         * This is the URL that users can
         * send to their friends.
         */

        await navigator.clipboard.writeText(
            previewUrl
        );


        const button =
            $('#copyLink');

        const original =
            button.textContent;


        button.textContent =
            '✓ Link Copied!';


        setTimeout(() => {

            button.textContent =
                original;

        }, 1800);

    };

$('#whatsapp').onclick = () => {

    if (!previewUrl) {
        return;
    }


    const message =
        encodeURIComponent(
            '🎉 I made a special birthday experience for you! Open this 👇\n\n'
            + previewUrl
        );


    const whatsappUrl =
        'https://wa.me/?text='
        + message;


    window.open(
        whatsappUrl,
        '_blank'
    );

};

show(1);