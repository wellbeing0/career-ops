import {recordOpportunityNote} from '../../web/src/lib/hosted/search-settings.mjs';
const root=process.argv[2];if(root!=='/var/lib/career-ops/brad')throw new Error('Fixed Brad root required');
console.log(JSON.stringify(recordOpportunityNote({root,candidate:'brad'},'https://job-boards.greenhouse.io/grafanalabs/jobs/6208010004','Steve reviewed the posting and reported that Grafana hires globally and is remote first (user-stated, October 3, 2026). This saved opening is listed as Canada Remote; eligibility for Brad to hold this specific role from Michigan has not been confirmed.')));
