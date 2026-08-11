const API = 'http://127.0.0.1:8000';

let step = 1,
    theme = 'surprise',
    intensity = 'crazy',
    html = '';

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

$('.themes').innerHTML = 'Cricket Legend|Classified Mystery|Movie Trailer|Game Mode|Heartfelt|Surprise Me'
    .split('|')
    .map((x, i) =>
        `<button type="button" data-v="${[
            'cricket',
            'mystery',
            'cinema',
            'gaming',
            'emotional',
            'surprise'
        ][i]}" class="${i === 5 ? 'selected' : ''}">
            ${['🏏', '🕵️', '🎬', '🎮', '❤️', '✨'][i]} ${x}
        </button>`
    )
    .join('');

$$('.themes button').forEach(b => {
    b.onclick = () => {
        $$('.themes button').forEach(x => x.classList.remove('selected'));
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
    let p = data();

    if (!p.name) {
        alert('Please enter their name.');
        return;
    }

    $('#form').style.display = 'none';
    $('.heading').style.display = 'none';
    $('.builder>label').style.display = 'none';
    $('#generating').classList.add('active');

    try {

        console.log('Sending birthday profile:', p);

        const r = await fetch(
            API + '/api/birthday/generate',
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(p)
            }
        );

        console.log(
            'Backend response:',
            r.status,
            r.statusText
        );


        /*
         * IMPORTANT:
         * Don't hide backend errors.
         */

        if (!r.ok) {

            const errorText =
                await r.text();

            console.error(
                'Backend error:',
                errorText
            );

            throw new Error(
                `Backend returned ${r.status}\n\n${errorText}`
            );
        }


        /*
         * Backend successfully generated
         * the birthday HTML.
         */

        html = await r.text();

        console.log(
            'Birthday experience generated successfully.'
        );


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
            'Birthday generation failed:',
            error
        );


        $('#form').style.display = '';
        $('.heading').style.display = '';


        /*
         * Show the ACTUAL problem.
         */

        alert(
            'Birthday generation failed.\n\n' +
            error.message
        );

    }
}

$('#next').onclick = () =>
    step < 4
        ? show(step + 1)
        : generate();

$('#back').onclick = () =>
    step > 1 && show(step - 1);

$('#open').onclick = () =>
    window.open(
        URL.createObjectURL(
            new Blob([html], { type: 'text/html' })
        ),
        '_blank'
    );

show(1);