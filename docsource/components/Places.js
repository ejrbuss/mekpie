import Link  from 'next/link';
import Vars  from '../Vars'; 

export default ({ home, api }) => (
    <>
        <Link href={Vars.sitePrefix + '/index'}><a className={`m-md ${home ? 'active' : ''}`}><i className='fas fa-home' />Home</a></Link>
    </>
);