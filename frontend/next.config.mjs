/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://royals-intelligence-api.onrender.com/api/v1';
    return [
      {
        source: '/api/v1/:path*',
        destination: `${backendUrl.replace(/\/+$/, '')}/:path*`,
      },
    ];
  },
};

export default nextConfig;
