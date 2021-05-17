# Build environment
FROM node:alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json .
COPY package-lock.json .
RUN npm install -g npm@7.13.0
RUN npm ci
COPY . .
RUN npm run build

# Execution environment
FROM node:alpine
WORKDIR /app
COPY --from=build /app/build /app/build
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json .
COPY package-lock.json .
RUN npm install -g npm@7.13.0
RUN npm ci --production
ENTRYPOINT ["npm", "run", "check"]
CMD ["jita"]
