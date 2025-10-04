/** @type {import('next').NextConfig} */
const nextConfig = {
  // Railway 배포를 위한 설정 - 정적 export로 변경하여 리소스 절약
  output: 'export',
  
  // 이미지 최적화 설정
  images: {
    domains: ['localhost'],
    unoptimized: true, // 정적 export에서 필수
  },

  // 환경 변수 설정
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },

  // 실험적 기능들
  experimental: {
    // 서버 컴포넌트 최적화
    serverComponentsExternalPackages: [],
  },

  // 압축 및 최적화
  compress: true,
  poweredByHeader: false,

  // Railway에서 정적 파일 서빙을 위한 설정
  trailingSlash: false,
  
  // API 경로 재작성 (필요시)
  async rewrites() {
    return [
      // Flask 백엔드로의 프록시 설정
      {
        source: '/api/backend/:path*',
        destination: process.env.FLASK_SERVER_URL ? `${process.env.FLASK_SERVER_URL}/api/:path*` : '/api/:path*',
      },
    ];
  },

  // 헤더 설정
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
